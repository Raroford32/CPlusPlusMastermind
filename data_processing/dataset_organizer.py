import re
import os
from database.db_operations import get_all_code_samples, update_code_sample

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

def analyze_project_structure(structured_samples):
    for directory, contents in structured_samples.items():
        if isinstance(contents, dict):
            files = [f for f in contents.keys() if not isinstance(contents[f], dict)]
            
            # Analyze build system
            if 'CMakeLists.txt' in files:
                contents['build_system'] = 'CMake'
            elif 'Makefile' in files:
                contents['build_system'] = 'Make'
            elif 'requirements.txt' in files:
                contents['build_system'] = 'Python'
            elif 'package.json' in files:
                contents['build_system'] = 'Node.js'
            
            # Analyze dependencies
            dependencies = set()
            for file in files:
                with open(file, 'r') as f:
                    content = f.read()
                    if file == 'requirements.txt':
                        dependencies.update(line.strip() for line in content.splitlines())
                    elif file == 'package.json':
                        import json
                        package_data = json.loads(content)
                        dependencies.update(package_data.get('dependencies', {}).keys())
            
            contents['dependencies'] = list(dependencies)
            
            analyze_project_structure(contents)

def organize_dataset():
    samples = get_all_code_samples()
    structured_samples = {}
    
    for sample in samples:
        categories = categorize_sample(sample['content'], sample['language'], sample['file_type'])
        complexity = calculate_complexity(sample['content'])
        
        sample['categories'] = categories
        sample['complexity'] = complexity
        
        # Build the structured samples
        parts = sample['filename'].split('/')
        current_dict = structured_samples
        for part in parts[:-1]:
            if part not in current_dict:
                current_dict[part] = {}
            current_dict = current_dict[part]
        current_dict[parts[-1]] = sample
        
        update_code_sample(sample)
    
    analyze_project_structure(structured_samples)
    
    return structured_samples

if __name__ == '__main__':
    organize_dataset()
