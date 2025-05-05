import {useEffect, useState, useContext} from "react";
import {ActiveSaveContext} from "../../providers/ActiveSaveProvider.tsx";
import {getSaveGameSectors} from "../../functions/responses.ts";
import TextField from "@mui/material/TextField";
import {Autocomplete} from "@mui/material";

export default function SectorsAutoComplete() {
  const activeSave = useContext(ActiveSaveContext);
  const [loading, setLoading] = useState(true)
  const [sectors, setSectors] = useState<any>()

  useEffect(() => {
    setLoading(true)
    getSaveGameSectors(activeSave.activeSave.id).then((response: Array<object>) => {
      const options = response.map(sector => ({id: sector.id, label: sector.name}))
      setSectors(options)
      setLoading(false)
    })
  }, []);

  return (
    <Autocomplete
      options={sectors}
      sx={{width: 300}}
      renderInput={(params) => <TextField {...params} label="Choose a sector" />}
    />
  )
}