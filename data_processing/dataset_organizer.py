from database.db_operations import get_all_code_samples, update_code_sample
import re

def categorize_sample(content, language, file_type):
    categories = [file_type]  # Start with the file_type (frontend, backend, database)
    
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
    
    # Categorize by specific technologies or frameworks
    if language == 'python':
        if 'flask' in content.lower():
            categories.append('flask')
        elif 'django' in content.lower():
            categories.append('django')
    elif language == 'javascript':
        if 'react' in content.lower():
            categories.append('react')
        elif 'vue' in content.lower():
            categories.append('vue')
        elif 'angular' in content.lower():
            categories.append('angular')
    elif language == 'html':
        categories.append('markup')
    elif language == 'css':
        categories.append('styling')
    elif language in ['sql', 'mysql', 'postgresql']:
        categories.append('database_query')
    
    # Categorize by complexity
    loc = len(content.splitlines())
    if loc < 50:
        categories.append('simple')
    elif 50 <= loc < 200:
        categories.append('moderate')
    else:
        categories.append('complex')
    
    return categories

def calculate_complexity(content):
    # Enhanced complexity calculation
    branches = len(re.findall(r'\b(if|for|while|case)\b', content))
    functions = len(re.findall(r'\b(def|function)\b', content))
    classes = len(re.findall(r'\bclass\b', content))
    return 1 + branches + (2 * functions) + (3 * classes)

def organize_dataset():
    samples = get_all_code_samples()
    
    for sample in samples:
        categories = categorize_sample(sample['content'], sample['language'], sample['file_type'])
        complexity = calculate_complexity(sample['content'])
        
        sample['categories'] = categories
        sample['complexity'] = complexity
        
        update_code_sample(sample)

if __name__ == '__main__':
    organize_dataset()
