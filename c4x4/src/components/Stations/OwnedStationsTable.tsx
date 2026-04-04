import {useContext, useEffect, useState} from "react";
import {ActiveSaveContext} from "../../contexts/ActiveSaveProvider.tsx";
import {DataGrid, GridColDef} from "@mui/x-data-grid";
import {OnHoverDelete} from "../DeleteButton.tsx";
import {deleteOwnedStation, getSaveGameStations} from "../../functions/responses.ts";
import {Skeleton} from "@mui/material";
import Box from "@mui/material/Box";

type StationRow = {
  id: number,
  name: string,
  population: number,
}

export default function OwnedStationsTable({ ...props}) {
  const [stations, setStations] = useState<any>()
  const [loading, setLoading] = useState(true)
  const activeSaveContext = useContext(ActiveSaveContext)
  const activeSave = useContext(ActiveSaveContext)
  const sectorColumns: GridColDef<StationRow>[] = [
    {
      field: 'name',
      headerName: 'Sector Name',
      flex: 5,
    },
    {
      field: 'population',
      headerName: 'Population',
      flex: 2,
    },
    {
      field: 'action',
      headerName: 'Action',
      flex: 1,
      sortable: false,
      filterable: false,
      renderCell: (params) => (
        <OnHoverDelete onClick={() => {
          if (!activeSave.activeSave.id) {
            return
          }
          deleteOwnedStation(activeSave.activeSave.id, Number(params.id)).then()
        }}></OnHoverDelete>
      )
    }
  ]

  useEffect(() => {
    setLoading(true)
    if (!activeSave.activeSave.id) {
      setLoading(false)
      return
    }
    getSaveGameStations(activeSave.activeSave.id).then((response: object) => {
      setStations(response)
      setLoading(false)
    })
  }, [activeSaveContext.activeSave.id])

  return (
    <>
      {loading ? (
        <Skeleton variant="rectangular" height={400} />
      ) : (
        <Box sx={{ height: 400, width: '100%' }}>
          <DataGrid
            {...props}
            disableRowSelectionOnClick
            rows={stations}
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