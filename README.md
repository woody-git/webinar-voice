# Serverless solution per doppiaggio della voce

Nel webinar che ho tenuto il 22 gennaio 2019, dal titolo <i>"Analisi di audio e testo con i servizi gestiti di AI/ML di AWS"</i>, ho illustrato come implementare una soluzione serverless per trascrivere (Amazon Transcribe) un audio mp4 in italiano, tradurlo (Amazon Translate) in inglese e creare l'equivalente text-to-speech (Amazon Polly).<br>

I servizi sono integrati utilizzando due funzioni lambda, rispettivamente:

* <b>interpreter-demo-transcribe:</b> Lambda function che utilizza Amazon Transcribe per trascrivere l'audio di un file mp4, con saving della transcrizione su S3

* <b>voicesservices-demo-audioout:</b> Lambda function che integra Amazon Translate per tradurre la trascrizione dall'italiano all'inglese, per poi trasformare il testo della traduzione (text-to-speech) in file audio mp3, utilizzando Amazon Polly

Questa l'architettura di riferimento illustrata nel webinar

<img src="https://github.com/woody-git/webinar-voice/blob/master/images/Solution%20Architecture.png?raw=true"/>

Qui è possibile rivedere il webinar (previa registrazione): https://register.gotowebinar.com/register/626781397079402242
