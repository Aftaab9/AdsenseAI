"""
Check which files will be committed to GitHub
Run this before pushing to verify only essential files are included
"""

import os
import subprocess

def get_git_files():
    """Get list of files that will be committed"""
    try:
        # Initialize git if not already
        if not os.path.exists('.git'):
            print("Initializing git...")
            subprocess.run(['git', 'init'], check=True)
        
        # Add all files
        subprocess.run(['git', 'add', '.'], check=True)
        
        # Get list of files
        result = subprocess.run(
            ['git', 'ls-files'],
            capture_output=True,
            text=True,
            check=True
        )
        
        return result.stdout.strip().split('\n')
    except subprocess.CalledProcessError as e:
        print(f"Error: {e}")
        return []

def categorize_files(files):
    """Categorize files by type"""
    categories = {
        'Core App': [],
        'Analyzers': [],
        'Data Files': [],
        'Frontend': [],
        'Config': [],
        'Documentation': [],
        'Other': []
    }
    
    for file in files:
        if not file:
            continue
            
        if file.startswith('app/analyzers/'):
            categories['Analyzers'].append(file)
        elif file.startswith('app/'):
            categories['Core App'].append(file)
        elif file.startswith('Data/'):
            categories['Data Files'].append(file)
        elif file.startswith('templates/') or file.startswith('static/'):
            categories['Frontend'].append(file)
        elif file.endswith('.txt') or file.endswith('.yaml') or file.endswith('.json') or file == 'Procfile' or file == 'runtime.txt' or file == 'requirements.txt':
            categories['Config'].append(file)
        elif file.endswith('.md'):
            categories['Documentation'].append(file)
        else:
            categories['Other'].append(file)
    
    return categories

def main():
    print("=" * 60)
    print("Checking files that will be committed to GitHub...")
    print("=" * 60)
    print()
    
    files = get_git_files()
    
    if not files:
        print("No files found!")
        return
    
    categories = categorize_files(files)
    
    total = 0
    for category, file_list in categories.items():
        if file_list:
            print(f"\n{category} ({len(file_list)} files):")
            print("-" * 40)
            for file in sorted(file_list)[:10]:  # Show first 10
                print(f"  ✓ {file}")
            if len(file_list) > 10:
                print(f"  ... and {len(file_list) - 10} more")
            total += len(file_list)
    
    print()
    print("=" * 60)
    print(f"Total files to commit: {total}")
    print("=" * 60)
    print()
    
    # Check for unwanted files
    unwanted_patterns = ['test_', 'example_', 'debug_', 'demo_', '.bat', 'TASK_']
    unwanted = []
    
    for file in files:
        for pattern in unwanted_patterns:
            if pattern in file:
                unwanted.append(file)
                break
    
    if unwanted:
        print("⚠️  WARNING: Found potentially unwanted files:")
        for file in unwanted[:10]:
            print(f"  ⚠️  {file}")
        if len(unwanted) > 10:
            print(f"  ... and {len(unwanted) - 10} more")
        print()
        print("Consider adding these to .gitignore")
    else:
        print("✅ No unwanted files detected!")
    
    print()
    print("Next steps:")
    print("1. Review the files above")
    print("2. If looks good, run: git commit -m 'Initial commit'")
    print("3. Then follow DEPLOY_TO_GITHUB.md for pushing to GitHub")

if __name__ == "__main__":
    main()
