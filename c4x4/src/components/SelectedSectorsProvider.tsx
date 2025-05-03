import {createContext, useState} from "react"

type SelectedSectorsProviderProps = {
  selectedSectors: Array<number>
  setSelected: (sectors: Array<number>) => void
}

export const SelectedSectorsContext = createContext<SelectedSectorsProviderProps>({
  selectedSectors: [],
  setSelected: () => {}
})

export default function SelectedSectorsProvider({ children }: any) {
  const [selectedSectors, setSelectedSectors] = useState<Array<number>>([])

  const setSelected = (sectors: Array<number>) => {
    setSelectedSectors(sectors)
  }

  return (
    <SelectedSectorsContext.Provider value={{selectedSectors, setSelected}} >
      {children}
    </SelectedSectorsContext.Provider>
  )
}