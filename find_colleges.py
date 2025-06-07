import json

def find_computer_science_colleges(json_file, target_marks=185, eligible_categories=['BC', 'OC']):
    try:
        with open(json_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
            
        # Keywords for computer science related branches
        cs_keywords = [
            'computer', 'information', 'software', 'it', 'computing',
            'artificial', 'ai', 'machine learning', 'ml', 'data science',
            'data analytics', 'big data', 'cloud', 'cyber', 'intelligence'
        ]
        
        # Filter colleges with computer science branches, marks between 181-185, and eligible categories
        filtered_colleges = []
        for entry in data:
            try:
                marks = float(entry.get('AGGR MARK', '0'))
                branch = entry.get('Branch', '').lower()
                category = entry.get('ALLOTTED CATEGORY', '')
                
                # Check if it's a computer science related branch and eligible category
                is_cs_branch = any(keyword in branch for keyword in cs_keywords)
                is_eligible_category = category in eligible_categories
                is_in_range = 181 <= marks <= 185
                
                if is_cs_branch and is_in_range and is_eligible_category:
                    filtered_colleges.append({
                        'College': entry.get('College Details', ''),
                        'Branch': entry.get('Branch', ''),
                        'Marks': marks,
                        'Rank': entry.get(' RANK', ''),
                        'Category': category
                    })
            except (ValueError, TypeError):
                continue
        
        # Sort by marks in ascending order
        filtered_colleges.sort(key=lambda x: x['Marks'])
        
        # Get top 10 unique colleges
        seen_colleges = set()
        top_colleges = []
        
        for college in filtered_colleges:
            college_name = college['College']
            if college_name not in seen_colleges and len(top_colleges) < 10:
                seen_colleges.add(college_name)
                top_colleges.append(college)
        
        # Print results
        print(f"\nTop 10 Colleges for Computer Science/AI/Data Science (Cut-off Marks between 181-185):")
        print(f"Eligible Categories: {', '.join(eligible_categories)}")
        print("-" * 80)
        for i, college in enumerate(top_colleges, 1):
            print(f"\n{i}. College: {college['College']}")
            print(f"   Branch: {college['Branch']}")
            print(f"   Cut-off Marks: {college['Marks']}")
            print(f"   Rank: {college['Rank']}")
            print(f"   Category: {college['Category']}")
            print(f"   Chance of Admission: {'Moderate' if college['Marks'] < 183 else 'Low'}")
            print("-" * 80)
            
    except Exception as e:
        print(f"Error reading file: {str(e)}")

if __name__ == "__main__":
    find_computer_science_colleges("tneallotment.json") 