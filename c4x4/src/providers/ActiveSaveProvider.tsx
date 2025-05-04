import { createContext, useState } from "react";
import {setCookie} from "../functions/cookies.ts";

interface SaveGame {
  id: number | null;
  name: string | null
  dataset_id: number
}

type ActiveSaveContextProps = {
  activeSave: SaveGame
  setNewSave: (value: SaveGame) => void
}

export const ActiveSaveContext = createContext<ActiveSaveContextProps>({
  activeSave: {id: 1, name: null, dataset_id: 1},
  setNewSave: () => {}
});

export default function ActiveSaveProvider({ children }: any) {
  const [activeSave, setActiveSave] = useState<SaveGame>(
    {id: null, name: null, dataset_id: 1}
  )

  const setNewSave = (newSave: SaveGame) => {
    setActiveSave(newSave)
    setCookie('saveId', String(newSave.id))
    setCookie('datasetId', String(newSave.dataset_id))
  }

  return (
    <ActiveSaveContext.Provider value={{activeSave, setNewSave}}>
      {children}
    </ActiveSaveContext.Provider>
  )
}