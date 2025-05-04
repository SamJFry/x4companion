import {createContext, useState} from "react"

type OwnedSectorsContextProps = {
  sectorsChanged: boolean
  setChanged: (b: boolean) => void
}

export const OwnedSectorsContext = createContext<OwnedSectorsContextProps>({
  sectorsChanged: false,
  setChanged: () => {}
})

export default function OwnedSectorsProvider({ children }: any) {
  const [sectorsChanged, setSectorsChanged] = useState(false)

  const setChanged = (updated: boolean) => {
    setSectorsChanged(updated)
  }

  return (
    <OwnedSectorsContext.Provider value={{sectorsChanged, setChanged}}>
      {children}
    </OwnedSectorsContext.Provider>
  )
}
