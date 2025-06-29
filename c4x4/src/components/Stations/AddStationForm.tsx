import Grid from "@mui/material/Grid";
import SectorsAutoComplete from "../Sectors/SectorsAutoComplete.tsx";
import FactoryModuleAutoComplete from "../FactoryModules/FactoryModuleAutoComplete.tsx";
import OwnedSectorsProvider from "../Sectors/OwnedSectorsProvider.tsx";
import {Typography} from "@mui/material";
import FormFieldGrid from "../FormFields/AutoCompleteGrid.tsx";
import QuantityFieldAddon from "../FormFields/QuantityFieldAddon.tsx";
import AddCancelButtonPanel from "../Buttons/AddCancelButtonPanel.tsx";
import FormikTextField from "../FormFields/FormikTextField.tsx";
import { useFormikContext } from "formik";

export default function AddStationForm({ cancelAction, submitAction }) {
  const formik = useFormikContext()
  const submit = async () => {
    await formik.submitForm()
    console.log("submit")
  }
  return (
    <OwnedSectorsProvider>
      <Typography variant="h4" sx={{mb: 2}}>Create Station</Typography>
      <Typography fontWeight="bold">Location</Typography>
      <Grid container spacing={2} sx={{mb: 2}}>
        <Grid size={{ lg: 4, xs: 12 }}>
          <FormikTextField name="name" id="outlined-basic" label="Name" variant="outlined" fullWidth />
        </Grid>
        <Grid size={{ lg: 4, xs: 12 }}>
          <SectorsAutoComplete />
        </Grid>
      </Grid>
      <FormFieldGrid
        title="Factory Modules"
        field={<QuantityFieldAddon field={FactoryModuleAutoComplete}/>}
        sx={{mb: 2}}
      />
      <FormFieldGrid
        title="Habitat Modules"
        field={<QuantityFieldAddon field={FactoryModuleAutoComplete}/>}
      />
      <AddCancelButtonPanel addAction={submit} cancelAction={cancelAction} />
    </OwnedSectorsProvider>
  )
}