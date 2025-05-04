import Box from '@mui/material/Box'
import {Skeleton, Typography} from '@mui/material'
import {DataGrid, GridColDef} from '@mui/x-data-grid'
import { ActiveSaveContext } from "../providers/ActiveSaveProvider.tsx"
import { getWares } from "../functions/responses.ts";
import {useState, useEffect, useContext} from "react";

type WareRows = {
  id: number,
  name: string,
  storage: string,
  volume: number,
}

const WareColumns: GridColDef<WareRows>[] = [
  {
    field: 'name',
    headerName: 'Name',
    flex: 1
  },
  {
    field: 'storage',
    headerName: 'Storage Type',
    flex: 1
  },
  {
    field: 'volume',
    headerName: 'Volume m³',
    flex: 1
  },
]

export default function Wares() {
  const [wares, setWares] = useState<any>()
  const [loading, setLoading] = useState(true)
  const activeSaveContext = useContext(ActiveSaveContext)

  useEffect(() => {
    setLoading(true)
    let activeDataset = activeSaveContext.activeSave.dataset_id
    if (activeDataset) {
      getWares(activeDataset).then((response: object) => {
        setWares(response)
        setLoading(false)
      })
    }
  }, [activeSaveContext.activeSave.dataset_id])

  return (
    <Box sx={{ flexGrow: 1, m: '5%'}}>
      <Typography variant="h3">Wares</Typography>
      <Typography variant="subtitle1" sx={{ mb: 2 }}>
        View the available wares in the data set.
      </Typography>
      <Box sx={{ width: '100%' }}>
        {loading ? (
          <Skeleton variant="rectangular" height={400} />
        ) : (
          <DataGrid
            columns={WareColumns}
            rows={wares}
          />
        )}
      </Box>
    </Box>
  )
}