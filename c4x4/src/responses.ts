const backend: string = import.meta.env.VITE_BACKEND

export async function getUserToken(username: string, password: string): Promise<void | object> {
  const formData = new FormData()
  formData.append("username", username)
  formData.append("password", password)
  const request = await fetch(`${backend}/api/auth/`, {
    method: 'POST',
    body: formData
  })

  const response = await request.json()
  if (!("token" in response)) {
    return response
  }
  document.cookie = `token=Bearer ${response['token']}`
}

export async function getSaveGames() {
  const response = await fetch(`${backend}/game/`)
  const data = await response.json()
  console.log(response.status)
  return data["data"]
}

export async function getDatasets() {
  const response = await fetch(`${backend}/dataset/`, {
    method: 'GET',
    headers: {
      "Authorization": `${getCookie('token')}`
    }
  })
  if (response.status !== 200) {
    return "ERROR: Could not get datasets."
  }
  const data = await response.json()
  return data["data"]
}

export async function deleteSaveGame(gameId: Number) {
  const response = await fetch(`${backend}/game/${gameId}/`, {
    method: 'DELETE',
    headers: {
      "Authorization": `${getCookie('token')}`
    }
  })
  if (response.status !== 204) {
    return "ERROR: Could not process delete."
  }
  return response.status
}

function getCookie(name: String) {
  const value = `; ${document.cookie}`
  const parts = value.split(`; ${name}=`)
  if (parts.length === 2) {
    return parts.pop().split(';').shift();
  }
}