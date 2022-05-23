from django import template


register = template.Library()


@register.filter()
def censor(value):
   badwords = ('Алоха', 'пост', 'метис', 'привет')
   value = value.split()

   for index, word in enumerate(value):
      if any(badword in word for badword in badwords):
         value[index] = word[0] + "".join('*' if c.isalpha() else c for c in word)
         value[index] = value[index].replace('*', '', 1)
   return " ".join(value)
