import { SaveGame } from '../types.ts'
import { createContext, useState, useEffect } from "react";
import getCookie, {setCookie} from "../functions/cookies.ts";
import {getSaveGames} from "../functions/responses.ts";


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

  useEffect(() => {
    getSaveGames().then((response) => {
      const saveCookie = Number(getCookie('saveId'))
      const save = response.find((element: SaveGame) => element.id === saveCookie)
      if (save) {
        setActiveSave(save)
      }
    })
  }, []);

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