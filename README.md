<h1>Egyptian_id Info extractor</h1>

<h2> this version is not updated ask for the updated version</h2>

<h3>The project starts with Predicting whether it's an Egyptian Id or Not  by using Custom trained Yolov8 model</h3>

![r2](https://github.com/yassinmohamed111/egyptian-id-project/assets/108435195/e763238c-8d66-44c9-9a56-605d27632116)

<p>extract Firstname  , secondname , Location , National_id , Manfucture_id , Image </p>

<h3>After detection of the ID card and croping the Detected parts , there's some image preprocessing are done on them:</h3>

![output_manf](https://github.com/yassinmohamed111/egyptian-id-project/assets/108435195/6573a57c-89ac-4d25-b987-e30b6b635c22)

![output_id](https://github.com/yassinmohamed111/egyptian-id-project/assets/108435195/f5cb91f1-b420-4b9e-a23e-0d8be4c336c4)

![output_second_name](https://github.com/yassinmohamed111/egyptian-id-project/assets/108435195/61a37849-f077-4d8c-ab45-772cb1b47b86)

![output_name](https://github.com/yassinmohamed111/egyptian-id-project/assets/108435195/743737d5-c5b8-4b0b-83d1-adb6832657d2)

<h3>After preprocessing part used ocr arabic pytesseract to detect arabic letters and numerals and did some analysis on the ouptut to extract the useful data from the National_id  :</h3>

![Screenshot (1306)](https://github.com/yassinmohamed111/egyptian-id-project/assets/108435195/f64fbb08-c01a-4ad4-9b6c-da6b05bc1810)
