import {createContext, useState} from "react";

const OwnedSectorsContext = createContext()

export default function OwnedSectorsProvider({ children }: any) {
  const [sectorsChanged, setSectorsChanged] = useState(false)

  const setChanged = () => {
    setSectorsChanged(true)
    console.log("detected change")
    setSectorsChanged(false)
  }

  return (
    <OwnedSectorsContext.Provider value={{sectorsChanged, setChanged}}>
      {children}
    </OwnedSectorsContext.Provider>
  )
}
