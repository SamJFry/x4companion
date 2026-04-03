import { useContext, useState, useEffect } from 'react';
import { ActiveSaveContext } from "../../contexts/ActiveSaveProvider.tsx";
import { getHabitatModules } from "../../functions/responses.ts";
import {Autocomplete} from "@mui/material";
import Skeleton from "@mui/material/Skeleton";
import TextField from "@mui/material/TextField";

interface HabitatModule {
  name: string;
  id: string;
}

export default function HabitatModuleAutoComplete({...props}) {
  const activeSave = useContext(ActiveSaveContext);
  const [loading, setLoading] = useState(true);
  const [modules, setModules] = useState<Array<object>>([]);

  useEffect(() => {
    setLoading(true);
    getHabitatModules(activeSave.activeSave.dataset_id).then((response: HabitatModule[]) => {
      const options = response.map(module => ({key: module.id, label: module.name}))
      setModules(options)
      setLoading(false)
    })
  }, [activeSave.activeSave.id]);

  return (
    <>
      {loading ? (
        <Skeleton variant="rectangular" />
      ) : (
        <Autocomplete
          {...props}
          options={modules}
          renderInput={(params) => <TextField {...params} label="Choose a module" size="small" />}
        />
      )}
    </>
  )
}