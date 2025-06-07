from flask import Flask, render_template, request
import json
import re
from math import ceil

app = Flask(__name__)

# Helper function to filter colleges
from find_colleges import find_computer_science_colleges

CATEGORY_ELIGIBILITY = {
    'OC': ['OC'],
    'BC': ['OC', 'BC'],
    'MBC': ['OC', 'BC', 'MBC'],
    'SC': ['OC', 'BC', 'MBC', 'SC'],
    'ST': ['OC', 'BC', 'MBC', 'SC', 'ST']
}

def find_non_cs_colleges(json_file, target_marks=185, eligible_categories=['BC', 'OC']):
    try:
        with open(json_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
        filtered_colleges = []
        # Build a mapping from college name to all eligible branches
        college_to_branches = {}
        for entry in data:
            try:
                marks = float(entry.get('AGGR MARK', '0'))
                branch = entry.get('Branch', '').lower()
                category = entry.get('ALLOTTED CATEGORY', '')
                # Exclude computer science related branches
                cs_keywords = [
                    'computer', 'information', 'software', 'it', 'computing',
                    'artificial', 'ai', 'machine learning', 'ml', 'data science',
                    'data analytics', 'big data', 'cloud', 'cyber', 'intelligence'
                ]
                is_cs_branch = any(keyword in branch for keyword in cs_keywords)
                is_eligible_category = category in eligible_categories
                is_in_range = marks <= target_marks
                if not is_cs_branch and is_eligible_category and is_in_range:
                    college_name = entry.get('College Details', '')
                    if college_name not in college_to_branches:
                        college_to_branches[college_name] = []
                    college_to_branches[college_name].append(entry.get('Branch', ''))
            except (ValueError, TypeError):
                continue
        for college in data:
            try:
                marks = float(college.get('AGGR MARK', '0'))
                branch = college.get('Branch', '').lower()
                category = college.get('ALLOTTED CATEGORY', '')
                # Exclude computer science related branches
                cs_keywords = [
                    'computer', 'information', 'software', 'it', 'computing',
                    'artificial', 'ai', 'machine learning', 'ml', 'data science',
                    'data analytics', 'big data', 'cloud', 'cyber', 'intelligence'
                ]
                is_cs_branch = any(keyword in branch for keyword in cs_keywords)
                is_eligible_category = category in eligible_categories
                is_in_range = marks <= target_marks
                if not is_cs_branch and is_eligible_category and is_in_range:
                    filtered_colleges.append({
                        'College': college.get('College Details', ''),
                        'Branch': branch,
                        'Marks': marks,
                        'Rank': college.get(' RANK', ''),
                        'Category': category
                    })
            except (ValueError, TypeError):
                continue
        def extract_numeric_rank(rank):
            if not rank:
                return float('inf')
            match = re.match(r"(\d+)", str(rank).strip())
            if match:
                return float(match.group(1))
            return float('inf')
        filtered_colleges.sort(key=lambda x: extract_numeric_rank(x['Rank']))
        seen_colleges = set()
        all_colleges = []
        for college in filtered_colleges:
            college_name = college['College']
            if college_name not in seen_colleges:
                seen_colleges.add(college_name)
                # Add other eligible branches for this college
                other_branches = [b for b in college_to_branches.get(college_name, []) if b != college['Branch']]
                college['Other Eligible Branches'] = other_branches
                all_colleges.append(college)
        return all_colleges
    except Exception as e:
        return []

@app.route('/', methods=['GET'])
def index():
    # Get search parameters from query string
    cutoff = request.args.get('cutoff', type=float)
    category = request.args.get('category', default='OC')
    discipline = request.args.get('discipline', default='cs')
    page = request.args.get('page', default=1, type=int)
    per_page = 20
    colleges = []
    total = 0
    if cutoff is not None and category and discipline:
        eligible_categories = CATEGORY_ELIGIBILITY.get(category, ['OC'])
        if discipline == 'cs':
            colleges = find_computer_science_colleges('tneallotment.json', target_marks=cutoff, eligible_categories=eligible_categories)
        else:
            colleges = find_non_cs_colleges('tneallotment.json', target_marks=cutoff, eligible_categories=eligible_categories)
    total = len(colleges)
    start = (page - 1) * per_page
    end = start + per_page
    paginated_colleges = colleges[start:end]
    total_pages = ceil(total / per_page) if total else 1
    return render_template('index.html', colleges=paginated_colleges, page=page, total_pages=total_pages, total=total, cutoff=cutoff, category=category, discipline=discipline)

if __name__ == '__main__':
    app.run(debug=True) 