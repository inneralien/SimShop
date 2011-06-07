email_template = \
"""
<?xml version="1.0" encoding="utf-8" ?>
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" xml:lang="en" lang="en">
  <head>
    <meta http-equiv="Content-Type" content="text/html; charset=UTF-8" />
    <style type="text/css">
    $css_style
    </style>
  </head>
  <body>
    <h1>$date</h1>
    <div id="content">
    <pre>
$tree
$tally
    </pre>
    </div>
  </body>
</html>
"""

fancy_template = \
"""
<?xml version="1.0" encoding="utf-8" ?>
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" xml:lang="en" lang="en">
    <head>
        <meta http-equiv="Content-Type" content="text/html; charset=UTF-8" />
        <style type="text/css">
        $css_style
        </style>
    </head>
    <body>
        <table border="0" cellpadding="20" cellspacing="0" width="100%">
            <tr>
                <td valign="top">
                    <div mc:edit="std_content00">
                    <h2 class="h2">$date</h2>
                    <pre>
$tree
$tally
                    </pre>
                    </div>
                </td>
            </tr>
        </table>
    </body>
    </html>
"""
