import argparse
from data_collection.github_scraper import scrape_github
from data_collection.stackoverflow_scraper import scrape_stackoverflow
from data_collection.website_scraper import scrape_websites
from data_processing.code_cleaner import clean_and_deduplicate_samples
from data_processing.dataset_organizer import organize_dataset
from model_fine_tuning.fine_tune import fine_tune_model

def main():
    parser = argparse.ArgumentParser(description="Full-stack C++ and Python Dataset Creation and Model Fine-tuning")
    parser.add_argument("--collect", action="store_true", help="Collect code samples")
    parser.add_argument("--process", action="store_true", help="Process and organize collected samples")
    parser.add_argument("--fine-tune", action="store_true", help="Fine-tune the model")
    
    args = parser.parse_args()

    if args.collect:
        print("Collecting code samples from full-stack repositories and tutorials...")
        scrape_github()
        scrape_stackoverflow()
        scrape_websites()
        print("Code sample collection completed.")

    if args.process:
        print("Processing and organizing code samples...")
        structured_samples = clean_and_deduplicate_samples()
        organized_samples = organize_dataset()
        print("Code sample processing and organization completed.")
        print(f"Total number of structured samples: {len(structured_samples)}")
        print(f"Total number of organized samples: {len(organized_samples)}")

    if args.fine_tune:
        print("Fine-tuning the model on full-stack and complex codebases...")
        fine_tune_model()
        print("Model fine-tuning completed.")

    if not any(vars(args).values()):
        print("No action specified. Use --collect, --process, or --fine-tune")

if __name__ == "__main__":
    main()
