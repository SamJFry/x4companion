import getCookie, {setCookie} from "./cookies.ts";

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
  setCookie('token', `Bearer ${response['token']}`)
}

export async function getSaveGames() {
  const response = await fetch(`${backend}/game/`)
  const data = await response.json()
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

export async function createSaveGame(name: String, dataset: number) {
  await fetch(`${backend}/game/`, {
    method: 'POST',
    headers: {
      "Authorization": `${getCookie('token')}`,
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      name: name,
      dataset_id: dataset
    })
  })
}

export async function getSectorTemplates(dataset: number) {
 const params = new URLSearchParams({page_size: '1000'})
  const response = await fetch(`${backend}/dataset/${dataset}/sector-templates?${params}`, {
    method: 'GET',
    headers: {
      "Authorization": `${getCookie('token')}`,
    },
  })
  if (response.status !== 200) {
    return "ERROR: Could not get sectors."
  }
  const data = await response.json()
  return data.data
}

export async function getSaveGameSectors(save: number) {
  const params = new URLSearchParams({page_size: '1000'})
  const response = await fetch(`${backend}/game/${save}/sectors?${params}`, {
    method: 'GET',
    headers: {
      "Authorization": `${getCookie('token')}`,
    },
  })
  if (response.status !== 200) {
    return "ERROR: Could not get sectors."
  }
  const data = await response.json()
  return data.data
}


export async function addOwnedSectors(save: number, sectors: Array<number>) {
  const response = await fetch(`${backend}/game/${save}/sectors/`, {
    method: 'POST',
    headers: {
      "Authorization": `${getCookie('token')}`,
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      data: sectors.map(id => ({template_id: id}))
    })
  })
  if (response.status !== 200) {
    return "ERROR: Could not add sectors."
  }
}

export async function deleteOwnedSectors(save: number, sectorId: number) {
  const response = await fetch(`${backend}/game/${save}/sectors/${sectorId}/`, {
    method: 'DELETE',
    headers: {
      "Authorization": `${getCookie('token')}`,
    }
  })
  if (response.status !== 204) {
    return "ERROR: Could not process delete."
  }
  return response.status
}

export async function getFactoryModules(dataset: number) {
  const params = new URLSearchParams({page_size: '1000'})
  const response = await fetch(`${backend}/dataset/${dataset}/factory-modules/?${params}`, {
    method: 'GET',
    headers: {
      "Authorization": `${getCookie('token')}`,
    }
  })
  if (response.status !== 200) {
    return "ERROR: Could not get factory modules."
  }
  const data = await response.json()
  return data.data
}

export async function getHabitatModules(dataset: number) {
  const params = new URLSearchParams({page_size: '1000'})
  const response = await fetch(`${backend}/dataset/${dataset}/habitat-modules/?${params}`, {
    method: 'GET',
    headers: {
      "Authorization": `${getCookie('token')}`,
    }
  })
  if (response.status !== 200) {
    return "ERROR: Could not get factory modules."
  }
  const data = await response.json()
  return data.data
}

export async function getWares(dataset: number) {
  const params = new URLSearchParams({page_size: '1000'})
  const response = await fetch(`${backend}/dataset/${dataset}/wares/?${params}`, {
    method: 'GET',
    headers: {
      "Authorization": `${getCookie('token')}`,
    }
  })
  if (response.status !== 200) {
    return "ERROR: Could not get wares."
  }
  const data = await response.json()
  return data.data
}