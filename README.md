# ChineseWordSegmentation
Chinese word segmentation algorithm without corpus

## Usage
```
from wordseg import wordSegment
doc = u'十四是十四四十是四十，十四不是四十，四十不是十四'
wordSegment(doc, max_word_len=2, min_aggregation=1, min_entropy=0.5)
```

This will generate words `十四`, `四十`, `不是`

In fact, `doc` should be a long enough document string for better results. In that condition, the min_aggregation should be set far greater than 1, such as 50, and min_entropy should also be set greater than 0.5, such as 1.5.

Besides, both input and output of this function should be decoded as unicode.

## Reference

Thanks Matrix67's [article](http://www.matrix67.com/blog/archives/5044)