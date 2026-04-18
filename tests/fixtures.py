"""Minimal HTML fixture mirroring the actual Power NI unit rates page structure."""

MOCK_HTML = """
<html><body>

<div class="grid-container">
  <div class="small-text-center sub-text" id="eco-energy">
    <h3 class="sub-title">Eco Energy</h3>
  </div>
  <table class="tbl-rates unit-rates">
    <thead><tr><th>Payment method</th><th>Discount</th><th>Unit rate (excl. VAT)</th><th>Unit rate (incl. VAT)</th></tr></thead>
    <tbody>
      <tr class="green-outline">
        <td class="best-deal best-deal--green"><span class="lbl-best">Best Deal</span>Monthly Direct Debit with online billing</td>
        <td>Up to &#xA3;60</td>
        <td class="center">28.78p*</td>
        <td class="center">30.22p*</td>
      </tr>
      <tr><td>Standard</td><td>-</td><td class="center">30.62p*</td><td class="center">32.15p*</td></tr>
    </tbody>
  </table>
</div>

<div class="grid-container">
  <div class="small-text-center sub-text" id="bill-pay">
    <h3 class="sub-title">Bill Pay</h3>
  </div>
  <table class="tbl-rates unit-rates">
    <thead><tr><th>Payment method</th><th>Discount</th><th>Unit rate (excl. VAT)</th><th>Unit rate (incl. VAT)</th></tr></thead>
    <tbody>
      <tr class="pink-outline">
        <td class="best-deal best-deal--pink"><span class="lbl-best">Best Deal</span>Monthly Direct Debit with online billing</td>
        <td>Up to &#xA3;60</td>
        <td class="center">28.78p*</td>
        <td class="center">30.22p*</td>
      </tr>
      <tr><td>Standard</td><td>-</td><td class="center">30.62p*</td><td class="center">32.15p*</td></tr>
    </tbody>
  </table>
</div>

<div class="grid-container">
  <div class="small-text-center sub-text" id="keypad">
    <h3 class="sub-title">Keypad</h3>
  </div>
  <table class="tbl-rates unit-rates">
    <thead><tr><th>Payment method</th><th>Discount</th><th>Unit rate (excl. VAT)</th><th>Unit rate (incl. VAT)</th></tr></thead>
    <tbody>
      <tr class="pink-outline">
        <td class="best-deal best-deal--pink"><span class="lbl-best">Best deal</span>Keypad reward &#xA3;150 top up</td>
        <td>2.5% plus &#xA3;4 free</td>
        <td class="center">29.07p*</td>
        <td class="center">30.53p*</td>
      </tr>
      <tr><td>Keypad</td><td>2.5%</td><td class="center">29.85p</td><td class="center">31.34p</td></tr>
    </tbody>
  </table>
</div>

<div class="grid-container">
  <div class="small-text-center sub-text" id="electric-vehicle-anytime">
    <h3 class="sub-title">Electric Vehicle Anytime</h3>
  </div>
  <table class="tbl-rates tbl-rates--multiline unit-rates">
    <thead><tr><th>Payment method</th><th>Discount</th><th>Time band</th><th>Unit rate (excl. VAT)</th><th>Unit rate (incl. VAT)</th></tr></thead>
    <tbody class="pink-outline">
      <tr>
        <td rowspan="2" class="best-deal best-deal--pink"><span class="lbl-best">Best Deal</span>Monthly Direct Debit with online billing</td>
        <td rowspan="2">Up to &#xA3;60</td>
        <td><span>Day rate</span></td>
        <td class="center">27.47p*</td>
        <td class="center">28.84p*</td>
      </tr>
      <tr>
        <td><span>Standing charge</span></td>
        <td class="center">11.53p*</td>
        <td class="center">12.10p*</td>
      </tr>
    </tbody>
  </table>
</div>

<div class="grid-container">
  <div class="small-text-center sub-text" id="electric-vehicle-nightshift">
    <h3 class="sub-title">Electric Vehicle Nightshift</h3>
  </div>
  <table class="tbl-rates tbl-rates--multiline unit-rates">
    <thead><tr><th>Payment method</th><th>Discount</th><th>Time band</th><th>Unit rate (excl. VAT)</th><th>Unit rate (incl. VAT)</th></tr></thead>
    <tbody class="pink-outline">
      <tr>
        <td rowspan="3" class="best-deal best-deal--pink"><span class="lbl-best">Best Deal</span>Monthly Direct Debit with online billing</td>
        <td rowspan="3">Up to &#xA3;60</td>
        <td><span>Night rate</span></td>
        <td class="center">16.00p*</td>
        <td class="center">16.80p*</td>
      </tr>
      <tr>
        <td><span>Day rate</span></td>
        <td class="center">33.46p*</td>
        <td class="center">35.14p*</td>
      </tr>
      <tr>
        <td><span>Standing charge</span></td>
        <td class="center">11.53p*</td>
        <td class="center">12.10p*</td>
      </tr>
    </tbody>
  </table>
</div>

<div class="grid-container">
  <div class="small-text-center sub-text" id="bill-pay-economy-7">
    <h3 class="sub-title">Bill Pay Economy 7</h3>
  </div>
  <table class="tbl-rates tbl-rates--multiline unit-rates">
    <thead><tr><th>Payment method</th><th>Discount</th><th>Time band</th><th>Unit rate (excl. VAT)</th><th>Unit rate (incl. VAT)</th></tr></thead>
    <tbody class="pink-outline">
      <tr>
        <td rowspan="3" class="best-deal best-deal--pink"><span class="lbl-best">Best Deal</span>Monthly Direct Debit with online billing</td>
        <td rowspan="3">Up to &#xA3;60</td>
        <td><span>Day</span></td>
        <td class="center">33.49p*</td>
        <td class="center">35.17p*</td>
      </tr>
      <tr>
        <td><span>Night</span></td>
        <td class="center">16.01p*</td>
        <td class="center">16.81p*</td>
      </tr>
      <tr>
        <td><span>Standing charge</span></td>
        <td class="center">11.53p*</td>
        <td class="center">12.10p*</td>
      </tr>
    </tbody>
  </table>
</div>

<div class="grid-container">
  <div class="small-text-center sub-text" id="keypad-economy-7">
    <h3 class="sub-title">Keypad Economy 7</h3>
  </div>
  <table class="tbl-rates tbl-rates--multiline unit-rates">
    <thead><tr><th>Payment method</th><th>Discount</th><th>Time band</th><th>Unit rate (excl. VAT)</th><th>Unit rate (incl. VAT)</th></tr></thead>
    <tbody class="pink-outline">
      <tr>
        <td rowspan="3" class="best-deal best-deal--pink"><span class="lbl-best">Best Deal</span>Keypad</td>
        <td rowspan="3">2.5%</td>
        <td><span>Day</span></td>
        <td class="center">34.76p*</td>
        <td class="center">36.50p*</td>
      </tr>
      <tr>
        <td><span>Night</span></td>
        <td class="center">16.62p*</td>
        <td class="center">17.45p*</td>
      </tr>
      <tr>
        <td><span>Standing charge</span></td>
        <td class="center">11.96p*</td>
        <td class="center">12.55p*</td>
      </tr>
    </tbody>
  </table>
</div>

</body></html>
"""
