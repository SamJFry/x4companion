const backend: string = import.meta.env.VITE_BACKEND

export async function getSaveGames() {
  const response = await fetch(`${backend}/game/`)
  const data = await response.json()
  console.log(response.status)
  return data["data"]
}