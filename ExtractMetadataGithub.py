from github import Github
import csv

# Replace 'YOUR_GITHUB_TOKEN' with your GitHub personal access token
#github_token = 'YOUR_GITHUB_TOKEN'

# Replace 'owner' and 'repo' with the GitHub owner and repository name
repo_owner = 'ashlinrajangabriel'
repo_name = 'SAPUI5_TS_NODEJS_APP'
#https://github.com/ashlinrajangabriel/SAPUI5_TS_NODEJS_APP
# Initialize the GitHub API client
g = Github()

# Get the repository object
repo = g.get_repo(f'{repo_owner}/{repo_name}')

# Open the CSV file for writing
csv_file = open('artifact_data.csv', 'w', newline='')
csv_writer = csv.writer(csv_file)

# Function to traverse the repository and retrieve artifacts' information
def traverse_repository(tree, prefix=''):
    for item in tree:
        # Check if it's a file
        if item.type == 'blob':
            # Retrieve the artifact information
            file_path = os.path.join(prefix, item.path)
            file_size = item.size
            last_modified = item.last_modified

            # Write the artifact information to the CSV file
            csv_writer.writerow([file_path, file_size, last_modified])

        # Check if it's a directory
        elif item.type == 'tree':
            # Recursively traverse the subdirectories
            traverse_repository(repo.get_git_tree(item.sha, recursive=True).tree, prefix=os.path.join(prefix, item.path))

# Get the root directory tree of the 'main' branch (you can replace 'main' with the desired branch name)
main_branch = repo.get_branch('main')
root_tree = repo.get_git_tree(main_branch.commit.sha, recursive=True).tree

# Start traversing the repository
traverse_repository(root_tree)

# Close the CSV file
csv_file.close()
