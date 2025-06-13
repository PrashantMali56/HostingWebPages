const {id} = await artifact.deleteArtifact(
  // name of the artifact
  'github-pages'
)

console.log(`Deleted Artifact ID '${id}'`)
