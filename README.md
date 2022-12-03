# Thesis: Civil Engineering Laboratory Automation and Systematization

<a href="https://youtu.be/DVeMYywfXPg">
   <img src="https://i.imgur.com/ji0btye.png" width="500">
</a>

## Project Description

**What it is?** 💡 A web application tool to automate and systematize trials at the Civil Engineering Laboratory. **Why did you build this project?** 💡 This was my thesis project for my professional degree. 

**What was my motivation?** 💡 This project was conceived in collaboration with my thesis tutor (Phd. Alejandro Hidalgo). He was enchage for the labs and I had learned a web development tools. **What did you learn?** 💡 Process identification and characterization, information analysis, system design, and programming the logic behind the primary chosen trials, how to create a basic user guide, how to generate results in web view and PDF, hands on HTML & CSS & JavaScript, use of Django as the main framework, SQLite data base, get some basic statistics on the frequency of some trials. Use PythonAnywhere servers to deploy the web applications.

## Table of Contents

<!--ts-->
* [Thesis: Civil Engineering Laboratory Automation and Systematization](#thesis-civil-engineering-laboratory-automation-and-systematization)
   * [Project Description](#project-description)
   * [Table of Contents](#table-of-contents)
   * [Thesis](#thesis)
      * [1. Presentation](#1-presentation)
      * [2. Documentation](#2-documentation)
      * [3. Some pictures of the EPIC Labs web application.](#3-some-pictures-of-the-epic-labs-web-application)
   * [How to Install and Run the Project](#how-to-install-and-run-the-project)
      * [1. Localy](#1-localy)
      * [2. Production](#2-production)
   * [How to ...](#how-to-)
      * [1. Contribute](#1-contribute)
      * [2. Use the Project](#2-use-the-project)
   * [Test](#test)
   * [+ Info](#-info)
   * [<em>Licence GNU GPLv3</em>](#licence-gnu-gplv3)

<!-- Created by https://github.com/ekalinin/github-markdown-toc -->
<!-- Added by: jorgeav527, at: Sat  3 Dec 00:04:28 -05 2022 -->

<!--te-->

## Thesis

### 1. Presentation

* Here is a [LINK](https://youtu.be/DVeMYywfXPg) to a YouTube video that supports the thesis.
* Here is a [LINK](https://www.dropbox.com/scl/fi/xra7o234a8lgu3zcqytsv/presentacion.odp?dl=0&rlkey=3yeq69q9d02qra1t9jqstp61x) to the PowerPoint presentation.

### 2. Documentation

* Here is a [LINK](https://www.dropbox.com/s/fyk09fv6cx1olh3/cara_map.pdf?dl=0) to the Process Characterization and the Management process flow map.
* Here is a [LINK](https://www.dropbox.com/s/pahfexskjut8ha5/tesis_alarcon_vargas_imprimir.pdf?dl=0) to the entire documentation.

### 3. Some pictures of the EPIC Labs web application.

* This is the first impression.

   <img src="https://i.imgur.com/fqsYD6y.jpg" width="600">

* Some features.

   <img src="https://i.imgur.com/Kg5oKLO.jpg" width="600">

* The labs.

   <img src="https://i.imgur.com/3OfSyYA.jpg" width="300">

* The users.

   <img src="https://i.imgur.com/RzVAnhT.jpg" width="300">

* First part of the trial.

   <img src="https://i.imgur.com/qH2G8Qe.jpg" width="600">

* Second part of the trial.

   <img src="https://i.imgur.com/38NmFIr.jpg" width="400">

* Results in a web browser part 1.

   <img src="https://i.imgur.com/hY1bVR9.jpg" width="400">

* Results in a web browser part 2

   <img src="https://i.imgur.com/Y0BCXLD.jpg" width="400">

* Results in a web browser if there is a graph part 3

   <img src="https://i.imgur.com/pju7O4Y.jpg" width="400">

* Results as a PDF report.

   <img src="https://i.imgur.com/hm7p6mS.jpg" width="600">

* Some statistics part 1.

   <img src="https://i.imgur.com/dYd0lvH.jpg" width="600">

* Some statistics part 2.

   <img src="https://i.imgur.com/oh03d13.jpg" width="400">

* Some statistics part 3.

   <img src="https://i.imgur.com/n8leMkq.jpg" width="600">

## How to Install and Run the Project

### 1. Localy

* Make a virtual environment and install the requirements.txt files.

    ```bash
    virtualenv venv
    source venv/bin/activate
    pip install -r requirements.txt
    ```

* Start the Django server, migrate and create a super user, it use the default SQLite database.

    ```bash
    django manage.py starserver
    django manage.py migrate
    django manage.py createsuperuser
    ```

### 2. Production

* You can follow the manual of [Deploying an existing Django project on PythonAnywhere](https://help.pythonanywhere.com/pages/DeployExistingDjangoProject/)
* Or watch this [YouTuBe](https://www.youtube.com/watch?v=1oOr7o3Cx1Y&t=50s) video

## How to ...

### 1. Contribute

* If you want to contribute or use the code, please do so and open a pull request. I am open to new ideas and opportunities.

### 2. Use the Project

* You can always refer to the presentation slides, documentation, or YouTube to learn more about the code's development. Please contact me at jorgeav@gmail.com if you require professional assistance with some code. 
* Just clone, fork and experiment.

## Test

ToDo

## + Info

- [How to Implement Multiple User Types with Django](https://simpleisbetterthancomplex.com/tutorial/2018/01/18/how-to-implement-multiple-user-types-with-django.html)
- [roles de usuarios en django](https://es.stackoverflow.com/questions/930/roles-de-usuarios-en-django)
- [creando registro de usuario e inicio de sesion con django](https://platzi.com/contributions/creando-registro-de-usuario-e-inicio-de-sesion-con-django/)
- [MDBootstrap](https://mdbootstrap.com/)
- [Jquery and Jquery UI](https://code.jquery.com/)
- [Django modales](http://pythonpiura.org/posts/modales-en-django-con-vistas-basadas-en-clases-y-jquery-ui/)
- [Maths](https://stackoverflow.com/questions/12165636/django-aggregation-summation-of-multiplication-of-two-fields)
- [Barcode](https://pythonhosted.org/pyBarcode/barcode.html#creating-barcodes-as-image)
- [To create a code for each test](https://www.djangorocks.com/snippets/creating-a-unique-slug.html)
- [Package models](https://stackoverflow.com/questions/49712889/how-to-create-a-package-of-models-in-django)
- [DropDown choice field](https://simpleisbetterthancomplex.com/tutorial/2018/01/29/how-to-implement-dependent-or-chained-dropdown-list-with-django.html)
- [make tabular data responsive](https://dbushell.com/2016/03/04/css-only-responsive-tables/)
- [responsive html table techniques](https://speckyboy.com/responsive-html-table-techniques/)
- [pdf files out of html templates with django](https://www.supinfo.com/articles/single/379-generate-pdf-files-out-of-html-templates-with-django)
- [weasyprint and bootstrap](https://stackoverflow.com/questions/32798998/weasyprint-and-bootstrap)
- [resistencia de prismas de albanileria](https://docplayer.es/43631805-Capitulo-5-resistencia-de-prismas-de-albanileria.html)
- [serving matplotlib graphs with django without saving](https://stackoverflow.com/questions/48286094/serving-matplotlib-graphs-with-django-without-saving)
- [matplotlib into a django](https://stackoverflow.com/questions/30531990/matplotlib-into-a-django-template?answertab=votes#tab-top)
- [add two arrays](https://www.geeksforgeeks.org/python-map-function/)
- [for naming table or columns in data base](https://stackoverflow.com/questions/28190564/custom-column-names-in-intermediary-table-for-many-to-many-model-in-django)
- [hilite](http://hilite.me/)
- [gravedad especifica de sólidos](https://www.yumpu.com/es/document/read/62948404/gravedad-especifica-de-sólidos-de-suelo-mediante-picnometro-de-agua)

## *Licence GNU GPLv3*