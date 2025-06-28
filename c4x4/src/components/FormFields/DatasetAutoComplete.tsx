import { useContext, useState, useEffect } from 'react';
import { ActiveSaveContext } from "../../contexts/ActiveSaveProvider.tsx";
import { getFactoryModules } from "../../functions/responses.ts";
import {Autocomplete} from "@mui/material";
import Skeleton from "@mui/material/Skeleton";
import TextField from "@mui/material/TextField";

type DataSetItem = {
  id: Number
  name: string
}

type DatasetAutoCompleteProps = {
  getDataFunction: (dataset: Number) => Promise<Array<DataSetItem>>
}

export default function DatasetAutoComplete({ getDataFunction }: DatasetAutoCompleteProps) {
  const activeSave = useContext(ActiveSaveContext);
  const [loading, setLoading] = useState(true);
  const [data, setData] = useState<Array<DataSetItem>>([]);

  useEffect(() => {
    setLoading(true);
    getDataFunction(activeSave.activeSave.dataset_id).then((response: Array<object>) => {
      const options = response.map(item => ({key: item.id, label: item.name}))
      setData(options)
      setLoading(false)
    })
  }, [activeSave.activeSave.id]);

  return (
    <>
      {loading ? (
        <Skeleton variant="rectangular" />
      ) : (
        <Autocomplete
          options={data}
          renderInput={(params) => <TextField {...params} label="Choose a module" />}
        />
      )}
    </>
  )
}