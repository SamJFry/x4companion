import { ReactNode, useState, useEffect } from 'react'
import Button from "@mui/material/Button";
import AddIcon from "@mui/icons-material/Add";
import Grid from "@mui/material/Grid";

type FormFieldGridProps = {
  field: ReactNode;
}

export default function FormFieldGrid({ field }: FormFieldGridProps) {
  const [fieldCount, setFieldCount] = useState<number>(0)
  const FieldComponent = field;

  return <>
    <Grid container spacing={2}>
      {Array.from({ length: fieldCount }).map(() => (
        <Grid size={{ lg: 4, xs: 12 }}>
          <FieldComponent />
        </Grid>
      ))}
    </Grid>
    <Button variant="contained" onClick={() => setFieldCount(fieldCount + 1)}>
      <AddIcon fontSize="small" />
    </Button>
  </>
}