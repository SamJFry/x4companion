import { SaveGame } from '../types.ts'
import { createContext, useState, useEffect } from "react";
import getCookie, {setCookie, deleteCookie} from "../functions/cookies.ts";
import {getSaveGames} from "../functions/responses.ts";


type ActiveSaveContextProps = {
  activeSave: SaveGame
  setNewSave: (value: SaveGame) => void
}

export const ActiveSaveContext = createContext<ActiveSaveContextProps>({
  activeSave: {id: null, name: null, dataset_id: 1},
  setNewSave: () => {}
});

export default function ActiveSaveProvider({ children }: any) {
  const [activeSave, setActiveSave] = useState<SaveGame>(
    {id: null, name: null, dataset_id: 1}
  )

  useEffect(() => {
    getSaveGames().then((response) => {
      const save = response[0]
      if (save) {
        setActiveSave(save)
      }
    })
  }, [activeSave.id ? null: activeSave]);

  const setNewSave = (newSave: SaveGame | null) => {
    if (!newSave) {
      setActiveSave({id: null, name: null, dataset_id: 1})
      deleteCookie('datasetId')
      return
    }
    setActiveSave(newSave)
    setCookie('datasetId', String(newSave.dataset_id))
  }

  return (
    <ActiveSaveContext.Provider value={{activeSave, setNewSave}}>
      {children}
    </ActiveSaveContext.Provider>
  )
}