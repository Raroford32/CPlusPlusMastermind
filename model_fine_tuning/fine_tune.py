from transformers import AutoTokenizer, AutoModelForCausalLM, Trainer, TrainingArguments
from datasets import Dataset
from database.db_operations import get_samples_for_fine_tuning

def prepare_dataset():
    samples = get_samples_for_fine_tuning()
    return Dataset.from_dict({
        'content': [sample['content'] for sample in samples],
        'language': [sample['language'] for sample in samples],
        'complexity': [sample['complexity'] for sample in samples]
    })

def tokenize_function(examples):
    return tokenizer(examples['content'], padding='max_length', truncation=True, max_length=512)

def fine_tune_model():
    # Load pre-trained model and tokenizer
    model_name = "microsoft/CodeGPT-small-py"  # You can change this to a different pre-trained model
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    model = AutoModelForCausalLM.from_pretrained(model_name)

    # Prepare and tokenize the dataset
    dataset = prepare_dataset()
    tokenized_dataset = dataset.map(tokenize_function, batched=True)

    # Set up training arguments
    training_args = TrainingArguments(
        output_dir="./results",
        num_train_epochs=3,
        per_device_train_batch_size=8,
        per_device_eval_batch_size=8,
        warmup_steps=500,
        weight_decay=0.01,
        logging_dir="./logs",
    )

    # Initialize Trainer
    trainer = Trainer(
        model=model,
        args=training_args,
        train_dataset=tokenized_dataset,
    )

    # Start fine-tuning
    trainer.train()

    # Save the fine-tuned model
    trainer.save_model("./fine_tuned_model")

if __name__ == "__main__":
    fine_tune_model()
