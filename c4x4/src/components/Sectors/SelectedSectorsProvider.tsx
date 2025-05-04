import {createContext, useState} from "react"
import {GridRowSelectionModel} from "@mui/x-data-grid";

type SelectedSectorsProviderProps = {
  selectedSectors: GridRowSelectionModel
  setSelected: (sectors: GridRowSelectionModel) => void
}

export const SelectedSectorsContext = createContext<SelectedSectorsProviderProps>({
  selectedSectors: [],
  setSelected: (_: GridRowSelectionModel) => {}
})

export default function SelectedSectorsProvider({ children }: any) {
  const [selectedSectors, setSelectedSectors] = useState<GridRowSelectionModel>([])

  const setSelected = (sectors: GridRowSelectionModel) => {
    setSelectedSectors(sectors)
  }

  return (
    <SelectedSectorsContext.Provider value={{selectedSectors, setSelected}} >
      {children}
    </SelectedSectorsContext.Provider>
  )
}