import {DataGrid, DataGridProps, GridColDef, GridRowSelectionModel} from "@mui/x-data-grid";
import {useEffect, useState, useContext} from "react";
import { SelectedSectorsContext } from "./SelectedSectorsProvider.tsx";
import { ActiveSaveContext } from "../../contexts/ActiveSaveProvider.tsx";
import {Skeleton} from "@mui/material";
import Box from "@mui/material/Box";

const sectorColumns: GridColDef<SectorRow>[] = [
  {
    field: 'name',
    headerName: 'Sector Name',
    width: 150,
  },
  {
    field: 'sunlight_percent',
    headerName: 'Sunlight Percent (%)',
    width: 150,
  },
]

type SectorRow = {
  id: number
  name: string
  sunlight_percent: number
}

type SectorDataGridProps = Omit<DataGridProps<SectorRow>, 'columns'>;

type SectorTableProps = {
  getFunction: (id: number) => Promise<Array<{}>>
} & SectorDataGridProps


export default function SectorsTable({ getFunction, ...dataGridProps }: SectorTableProps) {
  const [sectors, setSectors] = useState<any>()
  const [loading, setLoading] = useState(true)
  const selectedSectorsContext = useContext(SelectedSectorsContext)
  const activeSaveContext = useContext(ActiveSaveContext)

  useEffect(() => {
    setLoading(true)
    getFunction(activeSaveContext.activeSave.dataset_id).then((response: object) => {
      setSectors(response)
      setLoading(false)
    })
  }, [])

  const handleSelectionChange = (rowSelectionModel: GridRowSelectionModel) => {
    selectedSectorsContext.setSelected(rowSelectionModel)
  }
  return (
    <>
      {loading ? (
        <Skeleton variant="rectangular" height={400} />
      ) : (
        <Box sx={{ height: 400, width: '100%', mb: 2}}>
          <DataGrid
            {...dataGridProps}
            rows={sectors}
            columns={sectorColumns}
            onRowSelectionModelChange={handleSelectionChange}
            initialState={{
              pagination: {
                paginationModel: {
                  pageSize: 10
                }
              }
            }}
          />
        </Box>
      )}
    </>
  )
}