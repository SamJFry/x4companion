import {ElementType} from "react";
import TextField from "@mui/material/TextField";
import {Grid} from "@mui/material";

type QuantityFieldAddonProps = {
  field: ElementType;
}

export default function QuantityFieldAddon ({field}: QuantityFieldAddonProps) {
  const FieldComponent = field
  return (
    <Grid container spacing={0.5}>
      <Grid size={9}>
        <FieldComponent />
      </Grid>
      <Grid size={3}>
        <TextField type="number"/>
      </Grid>
    </Grid>
    )
}