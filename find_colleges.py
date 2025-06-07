import json
import re

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
        
        # Filter colleges with computer science branches, marks <= target_marks, and eligible categories
        filtered_colleges = []
        for entry in data:
            try:
                marks = float(entry.get('AGGR MARK', '0'))
                branch = entry.get('Branch', '').lower()
                category = entry.get('ALLOTTED CATEGORY', '')
                
                # Check if it's a computer science related branch and eligible category
                is_cs_branch = any(keyword in branch for keyword in cs_keywords)
                is_eligible_category = category in eligible_categories
                is_in_range = marks <= target_marks
                
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
        
        # Sort by student rank (ascending, best rank first)
        def extract_numeric_rank(rank):
            if not rank:
                return float('inf')
            match = re.match(r"(\d+)", str(rank).strip())
            if match:
                return float(match.group(1))
            return float('inf')
        filtered_colleges.sort(key=lambda x: extract_numeric_rank(x['Rank']))
        
        # Build a mapping from college name to all eligible branches
        college_to_branches = {}
        for entry in data:
            try:
                marks = float(entry.get('AGGR MARK', '0'))
                branch = entry.get('Branch', '').lower()
                category = entry.get('ALLOTTED CATEGORY', '')
                is_eligible_category = category in eligible_categories
                is_in_range = marks <= target_marks
                if is_eligible_category and is_in_range:
                    college_name = entry.get('College Details', '')
                    if college_name not in college_to_branches:
                        college_to_branches[college_name] = []
                    college_to_branches[college_name].append(entry.get('Branch', ''))
            except (ValueError, TypeError):
                continue
        
        # Remove the top 10 unique colleges limit, return all eligible colleges ordered by rank
        seen_colleges = set()
        all_colleges = []
        for college in filtered_colleges:
            college_name = college['College']
            if college_name not in seen_colleges:
                seen_colleges.add(college_name)
                # Add other eligible branches for this college, ensure uniqueness
                other_branches = list({b for b in college_to_branches.get(college_name, []) if b != college['Branch']})
                college['Other Eligible Branches'] = other_branches
                all_colleges.append(college)
        return all_colleges
            
    except Exception as e:
        print(f"Error reading file: {str(e)}")

if __name__ == "__main__":
    find_computer_science_colleges("tneallotment.json") 