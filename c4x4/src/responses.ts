const backend: string = import.meta.env.VITE_BACKEND

export async function getSaveGames() {
  const response = await fetch(`${backend}/game/`)
  const data = await response.json()
  console.log(response.status)
  return data["data"]
}

export async function deleteSaveGame(gameId: Number) {
  const response = await fetch(`${backend}/game/${gameId}/`, {
    method: 'DELETE'
  })
  if (response.status !== 204) {
    return "ERROR: Could not process delete."
  }
  return response.status
}