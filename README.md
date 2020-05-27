# R Model

This is an modeling example to be used with SAS Viya, Jenkins and Docker. It's part of a proof of concept of a ModelOps workflow implemented with CI/CD characterisctics.

This is an R model which gathers data from the SAS environment through [SWAT](https://github.com/sassoftware/R-swat) package and registers in on "Model Manager" and automatically deploy it in a container service. 