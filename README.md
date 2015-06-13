# ChineseWordSegmentation
Chinese word segmentation algorithm without corpus

## Usage
```
from wordseg import WordSegment
doc = u'十四是十四四十是四十，十四不是四十，四十不是十四'
ws = WordSegment(doc, max_word_len=2, min_aggregation=1, min_entropy=0.5)
ws.segSentence(doc)
```

This will generate words

`十四 是 十四 四十 是 四十 ， 十四 不是 四十 ， 四十 不是 十四`

In fact, `doc` should be a long enough document string for better results. In that condition, the min_aggregation should be set far greater than 1, such as 50, and min_entropy should also be set greater than 0.5, such as 1.5.

Besides, both input and output of this function should be decoded as unicode.

`WordSegment.segSentence` has an optional argument `method`, with values `WordSegment.L`, `WordSegment.S` and `WordSegment.ALL`, means

+ `WordSegment.L`: if a long word that is combinations of several shorter words found, given only the long word.
+ `WordSegment.S`: given the several shorter words.
+ `WordSegment.ALL`: given both the long and the shorters.

## Reference

Thanks Matrix67's [article](http://www.matrix67.com/blog/archives/5044)