function Handler {
    Param(
        [Parameter(Mandatory = $true)]
        [FunctionContext]$fnContext,
        [Parameter(Mandatory = $true)]
        [FunctionResponse]$fnResponse
    )
  
    $data = $fnContext.Body
    if ([string]::IsNullOrEmpty($data)) {
        $out = $(Get-Module -ListAvailable |
                ForEach-Object {
                  'Module Name:{0}' -f $_
                Get-Command -Module $_.name -CommandType cmdlet, function |
                    ForEach-Object {
                      "`t{0}" -f $_.Name
                }
            })
        $fnResponse.Body = $out
    }
    else {
        $out = $(pwsh -c $data)
        $fnResponse.Body = $out
    } 
}
