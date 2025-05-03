import {DataGrid, DataGridProps, GridColDef} from "@mui/x-data-grid";
import {useEffect, useState} from "react";
import getCookie from "../functions/cookies.ts";
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
  sectorCookie: string
} & SectorDataGridProps

export default function SectorsTable({ getFunction, sectorCookie, ...dataGridProps }: SectorTableProps) {
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