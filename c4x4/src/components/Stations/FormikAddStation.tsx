import { Formik } from "formik";
import AddStationForm from "./AddStationForm";
import * as yup from 'yup';
import {addOwnedStation} from "../../functions/responses.ts";
import { ActiveSaveContext } from "../../contexts/ActiveSaveProvider.tsx";
import {useContext} from "react";


type FormikAddStationProps = {
  cancelAction: Function;
  submitAction: Function;
}

export default function FormikAddStation({ cancelAction, submitAction }: FormikAddStationProps) {
  const activeSave = useContext(ActiveSaveContext)
  const initialValues = {
    name: '',
    sector_id: '',
    factories: [],
    habitats: []
  }
  const validationSchema = yup.object().shape({
    name: yup.string().required("Name is a required field"),
    sector_id: yup.number().required("Sector is required")
  })

  return (<>
    <Formik
      initialValues={initialValues}
      validationSchema={validationSchema}
      onSubmit={values => {
        console.log(values)
        addOwnedStation(activeSave.activeSave.id, values).then(
          submitAction()
        )
      }}
    >
      <AddStationForm cancelAction={cancelAction} submitAction={submitAction} />
    </Formik>
  </>)
}