import {useContext, useEffect, useState} from "react";
import { OwnedSectorsContext } from "./OwnedSectorsProvider.tsx";
import { ActiveSaveContext } from "../../providers/ActiveSaveProvider.tsx"
import {getSaveGameSectors, deleteOwnedSectors} from "../../functions/responses.ts";
import getCookie from "../../functions/cookies.ts";
import {Skeleton} from "@mui/material";
import Box from "@mui/material/Box";
import {DataGrid, GridColDef} from "@mui/x-data-grid";
import {OnHoverDelete} from "../DeleteButton.tsx";

type SectorRow = {
  id: number
  name: string
  sunlight_percent: number
}

export default function OwnedSectorsTable({ ...dataGridProps }) {
  const [sectors, setSectors] = useState<any>()
  const [loading, setLoading] = useState(true)
  const ownedSectorsContext = useContext(OwnedSectorsContext)
  const activeSaveContext = useContext(ActiveSaveContext)
  const saveId = Number(getCookie('saveId'));
  const sectorColumns: GridColDef<SectorRow>[] = [
    {
      field: 'name',
      headerName: 'Sector Name',
      flex: 5,
    },
    {
      field: 'sunlight_percent',
      headerName: 'Sunlight Percent (%)',
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
          console.log(params)
          deleteOwnedSectors(saveId, Number(params.id)).then(
            ownedSectorsContext.setChanged(true)
          )
        }}></OnHoverDelete>
      )
    }
  ]

  useEffect(() => {
    setLoading(true)
    getSaveGameSectors(saveId).then((response: object) => {
      setSectors(response)
      setLoading(false)
    })
    ownedSectorsContext.setChanged(false)
  }, [ownedSectorsContext.sectorsChanged, activeSaveContext.activeSave])

  return (
    <>
      {loading ? (
        <Skeleton variant="rectangular" height={400} />
      ) : (
        <Box sx={{ height: 400, width: '100%' }}>
          <DataGrid
            {...dataGridProps}
            disableRowSelectionOnClick
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