from transformers import AutoTokenizer, AutoModelForCausalLM, Trainer, TrainingArguments, DataCollatorForLanguageModeling
from datasets import Dataset
from database.db_operations import get_samples_for_fine_tuning
import torch

def prepare_dataset():
    samples = get_samples_for_fine_tuning(limit=10000)  # Increased sample size
    return Dataset.from_dict({
        'content': [sample['content'] for sample in samples],
        'language': [sample['language'] for sample in samples],
        'complexity': [sample['complexity'] for sample in samples],
        'categories': [','.join(sample['categories']) for sample in samples]
    })

def tokenize_function(examples, tokenizer):
    return tokenizer(examples['content'], padding='max_length', truncation=True, max_length=1024)  # Increased max_length

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
        per_device_train_batch_size=4,  # Reduced batch size to accommodate larger model
        per_device_eval_batch_size=4,
        warmup_steps=500,
        weight_decay=0.01,
        logging_dir="./logs",
        fp16=True,  # Enable mixed precision training
        gradient_accumulation_steps=4,  # Gradient accumulation for larger effective batch size
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
