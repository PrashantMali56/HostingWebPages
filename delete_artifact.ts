import fetch from 'node-fetch';

const GITHUB_TOKEN = process.env.GITHUB_TOKEN; // Set your GitHub token as an environment variable
const REPO = ${{ github.repository }}; // Replace with your repository name
const ARTIFACT_ID = '3323905621'; // Replace with the artifact ID you want to delete

async function deleteArtifact() {
    const url = `https://api.github.com/repos/${REPO}/actions/artifacts/${ARTIFACT_ID}`;
    const response = await fetch(url, {
        method: 'DELETE',
        headers: {
            Authorization: `Bearer ${GITHUB_TOKEN}`,
            Accept: 'application/vnd.github+json',
        },
    });

    if (response.ok) {
        console.log(`Artifact ${ARTIFACT_ID} deleted successfully.`);
    } else {
        console.error(`Failed to delete artifact: ${response.statusText}`);
    }
}

deleteArtifact().catch((error) => {
    console.error('Error deleting artifact:', error);
});
