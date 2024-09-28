import re
import os
from database.db_operations import get_all_code_samples, update_code_sample

def clean_code(code):
    # Remove single-line comments
    code = re.sub(r'//.*?\n', '\n', code)
    
    # Remove multi-line comments
    code = re.sub(r'/\*.*?\*/', '', code, flags=re.DOTALL)
    
    # Remove empty lines
    code = '\n'.join(line for line in code.splitlines() if line.strip())
    
    # Remove leading/trailing whitespace
    code = code.strip()
    
    return code

def remove_duplicate_samples(samples):
    unique_samples = {}
    for sample in samples:
        content_hash = hash(sample['content'])
        if content_hash not in unique_samples:
            unique_samples[content_hash] = sample
    return list(unique_samples.values())

def preserve_directory_structure(samples):
    structured_samples = {}
    for sample in samples:
        parts = sample['filename'].split('/')
        current_dict = structured_samples
        for part in parts[:-1]:
            if part not in current_dict:
                current_dict[part] = {}
            current_dict = current_dict[part]
        current_dict[parts[-1]] = sample
    return structured_samples

def clean_and_deduplicate_samples():
    samples = get_all_code_samples()
    cleaned_samples = []

    for sample in samples:
        cleaned_content = clean_code(sample['content'])
        if len(cleaned_content) >= 100:  # Increased minimum length threshold
            sample['content'] = cleaned_content
            cleaned_samples.append(sample)

    deduplicated_samples = remove_duplicate_samples(cleaned_samples)
    structured_samples = preserve_directory_structure(deduplicated_samples)

    for sample in deduplicated_samples:
        update_code_sample(sample)

    return structured_samples

if __name__ == '__main__':
    clean_and_deduplicate_samples()
