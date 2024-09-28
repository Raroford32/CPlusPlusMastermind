from database.db_operations import get_all_code_samples, update_code_sample
import re

def categorize_sample(content, language):
    categories = []
    
    # Categorize by application type
    if 'class' in content:
        categories.append('object_oriented')
    if 'def ' in content or 'function' in content:
        categories.append('functional')
    if 'import' in content or '#include' in content:
        categories.append('library_usage')
    if 'for' in content or 'while' in content:
        categories.append('loops')
    if 'if' in content:
        categories.append('conditional')
    
    # Categorize by complexity
    loc = len(content.splitlines())
    if loc < 20:
        categories.append('simple')
    elif 20 <= loc < 100:
        categories.append('moderate')
    else:
        categories.append('complex')
    
    # Add language category
    categories.append(language)
    
    return categories

def calculate_complexity(content):
    # Simple complexity calculation based on cyclomatic complexity
    branches = len(re.findall(r'\b(if|for|while|case)\b', content))
    return 1 + branches

def organize_dataset():
    samples = get_all_code_samples()
    
    for sample in samples:
        categories = categorize_sample(sample['content'], sample['language'])
        complexity = calculate_complexity(sample['content'])
        
        sample['categories'] = categories
        sample['complexity'] = complexity
        
        update_code_sample(sample)

if __name__ == '__main__':
    organize_dataset()
