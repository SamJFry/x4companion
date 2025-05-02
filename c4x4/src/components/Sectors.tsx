import Typography from '@mui/material/Typography'
import Box from '@mui/material/Box'
import { DataGrid, GridColDef } from "@mui/x-data-grid"
import { getSectorTemplates } from "../functions/responses.ts";
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

function SectorsTable({ endpoint, sectorCookie }) {
  const [sectors, setSectors] = useState()
  const [loading, setLoading] = useState(true)

  return <DataGrid
    rows={sectors}
    columns={sectorColumns}
  />
}

export default function Sectors() {
  const [sectors, setSectors] = useState()
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    setLoading(true)
    console.log(getCookie('datasetId'))
    getSectorTemplates(Number(getCookie('datasetId'))).then((response) => {
      setSectors(response)
      setLoading(false)
    })
  }, [])

  return (
    <>
      <Box sx={{ flexGrow: 1, m: '5%', }}>
        <Typography variant="h3">Sectors</Typography>
        <Typography variant="subtitle1">
          Manage the sectors that your empire has a presence in.
        </Typography>
        {loading ? (
          <Skeleton variant="rectangular" height={400} />
        ) : (
          <DataGrid
            rows={sectors}
            columns={sectorColumns}
          />
        )}
      </Box>
    </>
  )
}