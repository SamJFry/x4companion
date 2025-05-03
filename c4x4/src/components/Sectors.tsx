import Typography from '@mui/material/Typography'
import Box from '@mui/material/Box'
import { DataGrid, GridColDef, DataGridProps } from "@mui/x-data-grid"
import { getSaveGameSectors, getSectorTemplates } from "../functions/responses.ts";
import { useState, useEffect } from "react";
import {Skeleton} from "@mui/material";
import getCookie from "../functions/cookies.ts";

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
  sectorCookie: string
} & SectorDataGridProps

function SectorsTable({ getFunction, sectorCookie, ...dataGridProps }: SectorTableProps) {
  const [sectors, setSectors] = useState<any>()
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    setLoading(true)
    getFunction(Number(getCookie(sectorCookie))).then((response: object) => {
      setSectors(response)
      setLoading(false)
    })
  }, [])

  return (
    <>
      {loading ? (
        <Skeleton variant="rectangular" height={100} />
      ) : (
        <Box sx={{ height: 400, width: '100%', mb: 2}}>
          <DataGrid
            {...dataGridProps}
            rows={sectors}
            columns={sectorColumns}
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

export default function Sectors() {
  return (
    <>
      <Box sx={{ flexGrow: 1, m: '5%', }}>
        <Typography variant="h3">Sectors</Typography>
        <Typography variant="subtitle1">
          Manage the sectors that your empire has a presence in.
        </Typography>
        <SectorsTable getFunction={getSaveGameSectors} sectorCookie="saveId" />
        <SectorsTable getFunction={getSectorTemplates} sectorCookie="datasetId" checkboxSelection/>
      </Box>
    </>
  )
}