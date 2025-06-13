import * as artifact from '@actions/artifact';

async function deleteArtifact() {
    const artifactClient = artifact.create();
    const { id } = await artifactClient.deleteArtifact('github-pages'); // Replace 'artifact-name' with the actual name
    console.log(`Deleted artifact with ID: ${id}`);
}

deleteArtifact().catch((error) => {
    console.error('Error deleting artifact:', error);
});
