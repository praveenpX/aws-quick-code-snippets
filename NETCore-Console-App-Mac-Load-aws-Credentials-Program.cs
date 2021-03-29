/*
 * SPDX-License-Identifier: MIT-0
 *
 * Permission is hereby granted, free of charge, to any person obtaining a copy of this
 * software and associated documentation files (the "Software"), to deal in the Software
 * without restriction, including without limitation the rights to use, copy, modify,
 * merge, publish, distribute, sublicense, and/or sell copies of the Software, and to
 * permit persons to whom the Software is furnished to do so.
 *
 * THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED,
 * INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A
 * PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT
 * HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION
 * OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE
 * SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
 */

/*
*In the Program.cs file, you can use the following code snippet to load settings from 
*appsettings.json file and also load aws profile from mac aws credentials location
*DISCLAIMER: this is a sample snippet that is provide as is and is for informational
*purposes only. Test it thoroughly before using it
*/

using System;
using Microsoft.Extensions.Configuration;
using System.Collections.Generic;
using System.Threading.Tasks;
using Amazon.Runtime;
using Amazon.Runtime.CredentialManagement;
using Amazon.Extensions.NETCore.Setup;

namespace Sample {
	class Program {

		static void Main(string[] args)
		{
			var builder = new ConfigurationBuilder()
				.SetBasePath(Environment.CurrentDirectory)
				.AddJsonFile("appsettings.local.json", optional: false, reloadOnChange: true)
				.AddEnvironmentVariables()
				.Build();

			var awsOptions = builder.GetAWSOptions();
			var credentialProfileStoreChain = new CredentialProfileStoreChain();
			AWSCredentials defaultCredentials;
			if (credentialProfileStoreChain.TryGetAWSCredentials("default", out defaultCredentials))
			{
				awsOptions.Credentials = defaultCredentials;
			}

			else
			{
				throw new AmazonClientException("Unable to find a default profile in CredentialProfileStoreChain.");
			}
		}
	}



