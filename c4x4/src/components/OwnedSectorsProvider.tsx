import {createContext, useState} from "react";

type OwnedSectorsProviderProps = {
  sectorsChanged: boolean
  setChanged: () => void
}

export const OwnedSectorsContext = createContext<OwnedSectorsProviderProps>({
  sectorsChanged: false,
  setChanged: () => {}
})

export default function OwnedSectorsProvider({ children }: any) {
  const [sectorsChanged, setSectorsChanged] = useState(false)

  const setChanged = (update: boolean) => {
    setSectorsChanged(update)
  }

  return (
    <OwnedSectorsContext.Provider value={{sectorsChanged, setChanged}}>
      {children}
    </OwnedSectorsContext.Provider>
  )
}
