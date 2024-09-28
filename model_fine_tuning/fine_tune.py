from transformers import AutoTokenizer, AutoModelForCausalLM, Trainer, TrainingArguments, DataCollatorForLanguageModeling
from datasets import Dataset
from database.db_operations import get_samples_for_fine_tuning, get_project_structures
import torch

def prepare_dataset():
    samples = get_samples_for_fine_tuning(limit=10000)  # Increased sample size
    project_structures = get_project_structures()
    
    dataset = []
    for sample in samples:
        project_info = project_structures.get(sample['source'], {})
        dataset.append({
            'content': sample['content'],
            'language': sample['language'],
            'complexity': sample['complexity'],
            'categories': ','.join(sample['categories']),
            'file_type': sample['file_type'],
            'filename': sample['filename'],
            'build_system': project_info.get('build_system', ''),
            'dependencies': ','.join(project_info.get('dependencies', [])),
            'related_files': ','.join(sample.get('related_files', []))
        })
    
    return Dataset.from_dict({k: [d[k] for d in dataset] for k in dataset[0].keys()})

def tokenize_function(examples, tokenizer):
    # Combine all fields into a single text
    text = [f"Language: {lang}\nComplexity: {comp}\nCategories: {cat}\nFile Type: {ft}\nFilename: {fn}\nBuild System: {bs}\nDependencies: {dep}\nRelated Files: {rf}\n\nContent:\n{content}"
            for lang, comp, cat, ft, fn, bs, dep, rf, content in zip(examples['language'], examples['complexity'], 
                                                                     examples['categories'], examples['file_type'],
                                                                     examples['filename'], examples['build_system'],
                                                                     examples['dependencies'], examples['related_files'],
                                                                     examples['content'])]
    return tokenizer(text, padding='max_length', truncation=True, max_length=2048)  # Increased max_length

def fine_tune_model():
    # Load a larger pre-trained model
    model_name = "microsoft/CodeGPT-large-py"  # Using a larger model
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    model = AutoModelForCausalLM.from_pretrained(model_name)

    # Prepare and tokenize the dataset
    dataset = prepare_dataset()
    tokenized_dataset = dataset.map(lambda examples: tokenize_function(examples, tokenizer), batched=True)

    # Set up training arguments
    training_args = TrainingArguments(
        output_dir="./results",
        num_train_epochs=5,  # Increased number of epochs
        per_device_train_batch_size=2,  # Reduced batch size to accommodate larger model and context
        per_device_eval_batch_size=2,
        warmup_steps=500,
        weight_decay=0.01,
        logging_dir="./logs",
        fp16=True,  # Enable mixed precision training
        gradient_accumulation_steps=8,  # Increased gradient accumulation for larger effective batch size
        eval_steps=500,
        save_steps=1000,
        load_best_model_at_end=True,
    )

    # Data collator
    data_collator = DataCollatorForLanguageModeling(tokenizer=tokenizer, mlm=False)

    # Initialize Trainer
    trainer = Trainer(
        model=model,
        args=training_args,
        train_dataset=tokenized_dataset,
        data_collator=data_collator,
    )

    # Start fine-tuning
    trainer.train()

    # Save the fine-tuned model
    trainer.save_model("./fine_tuned_model")

if __name__ == "__main__":
    fine_tune_model()
