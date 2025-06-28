import Box from '@mui/material/Box'
import {Skeleton, Typography} from '@mui/material'
import {DataGrid, GridColDef} from '@mui/x-data-grid'
import { ActiveSaveContext } from "../contexts/ActiveSaveProvider.tsx"
import {getFactoryModules} from "../functions/responses.ts";
import {useState, useEffect, useContext} from "react";

type FactoryModuleRow = {
  id: number,
  name: string,
  ware_id: number,
  hourly_production: number,
  hourly_energy: number,
  workforce: number,
}

const FactoryModuleColumns: GridColDef<FactoryModuleRow>[] = [
  {
    field: 'name',
    headerName: 'Name',
    flex: 1
  },
  {
    field: 'hourly_production',
    headerName: 'Products per hour',
    flex: 1
  },
  {
    field: 'hourly_energy',
    headerName: 'Energy Cells per hour',
    flex: 1
  },
  {
    field: 'workforce',
    headerName: 'Workforce',
    flex: 1
  }
]

export default function FactoryModules() {
  const [modules, setModules] = useState<any>()
  const [loading, setLoading] = useState(true)
  const activeSaveContext = useContext(ActiveSaveContext)

  useEffect(() => {
    setLoading(true)
    let activeDataset = activeSaveContext.activeSave.dataset_id
    if (activeDataset) {
      getFactoryModules(activeDataset).then((response: object) => {
        setModules(response)
        setLoading(false)
      })
    }
  }, [activeSaveContext.activeSave.dataset_id])

  return (
    <Box sx={{ flexGrow: 1, m: '5%'}}>
      <Typography variant="h3">Factory Modules</Typography>
      <Typography variant="subtitle1" sx={{ mb: 2 }}>
        View the available factory modules in the data set.
      </Typography>
      <Box sx={{ width: '100%' }}>
        {loading ? (
          <Skeleton variant="rectangular" height={400} />
        ) : (
          <DataGrid
            columns={FactoryModuleColumns}
            rows={modules}
          />
        )}
      </Box>
    </Box>
  )
}