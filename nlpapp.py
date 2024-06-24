from elautil import nlputil as nlpu

doc = nlpu.make_doc('the cat ate the rat')
pos_info = nlpu.extract_pos_tags(doc)
print(pos_info)

#SpeechItem (id=activityid+studentid+packageId | audio file | timestamp)
#ProcessedSpeechItem (id, asr_text, asr_text_timings)
#TextItem (id, asr_text)
#ProcessedTextItem (id, text_metrics)

#ReportItem(id,alerts,)
#Insi -- how and when to capture historical analysis and resulting report item

#asr text post processing to remove hallucinations!