# ChineseWordSegmentation
Chinese word segmentation algorithm without corpus

## Usage
Suppose that `doc` is a long enough document string

```
from wordseg import wordSegment
wordSegment(u'十四是十四四十是四十，十四不是四十，四十不是十四', max_word_len=2, min_aggregation=1, min_entropy=0.5)
```

This will generate words `十四`, `四十`, `不是`

## Reference

Thanks Matrix67's [article](http://www.matrix67.com/blog/archives/5044)