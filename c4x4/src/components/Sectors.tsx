import Typography from '@mui/material/Typography'
import Box from '@mui/material/Box'
import { DataGrid, GridColDef } from "@mui/x-data-grid"
import {getSaveGameSectors, getSectorTemplates} from "../functions/responses.ts";
import {useState, useEffect} from "react";
import {Skeleton} from "@mui/material";
import getCookie from "../functions/cookies.ts";

const sectorColumns: GridColDef<(typeof rows)[number]>[] = [
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

interface SectorTableProps {
  getFunction: (id: number) => Promise<Array<{}>>
  sectorCookie: string
}

function SectorsTable({ getFunction, sectorCookie }: SectorTableProps) {
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
        <DataGrid
          height={100}
          rows={sectors}
          columns={sectorColumns}
          initialState={{
            pagination: {
              paginationModel: {
                pageSize: 5
              }
            }
          }}
        />
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
        <SectorsTable getFunction={getSectorTemplates} sectorCookie="datasetId" />
      </Box>
    </>
  )
}